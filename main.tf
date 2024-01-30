terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  shared_credentials_files = ["F:/Python/FYPRobotDog/mycode_20240120/key/aws_credentials.ini"]
}

resource "aws_s3_bucket" "fyp_iot_image" {
  bucket = "fyp-iot-image"
}

resource "aws_s3_object" "temp_folder" {
  bucket = aws_s3_bucket.fyp_iot_image.id
  key    = "temp/"
}

resource "aws_s3_object" "no_hat_folder" {
  bucket = aws_s3_bucket.fyp_iot_image.id
  key    = "no_hat/"
}

resource "aws_dynamodb_table" "iot_sensor" {
  name           = "IoT_sensor"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "sensor_id"
  range_key      = "timestamp"

  attribute {
    name = "sensor_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "sensor_type"
    type = "S"
  }

  attribute {
    name = "iot_device_id"
    type = "S"
  }

  global_secondary_index {
    name               = "sensor_type_index"
    hash_key           = "sensor_type"
    projection_type    = "ALL"
  }

 global_secondary_index {
    name               = "iot_device_id_index"
    hash_key           = "iot_device_id"
    projection_type    = "ALL"
  }
  lifecycle {
    ignore_changes = [read_capacity, write_capacity]
  }
}

##IoT Configure
resource "random_id" "id" {
	byte_length = 8
}

resource "aws_iot_thing" "thing" {
	name = "thing_${random_id.id.hex}"
}

output "thing_name" {
	value = aws_iot_thing.thing.name
}

resource "tls_private_key" "key" {
	algorithm   = "RSA"
	rsa_bits = 2048
}

resource "tls_self_signed_cert" "cert" {
	private_key_pem = tls_private_key.key.private_key_pem

	validity_period_hours = 240

	allowed_uses = [
	]

	subject {
		organization = "test"
	}
}

resource "aws_iot_certificate" "cert" {
	certificate_pem = trimspace(tls_self_signed_cert.cert.cert_pem)
	active          = true
}

resource "aws_iot_thing_principal_attachment" "attachment" {
	principal = aws_iot_certificate.cert.arn
	thing     = aws_iot_thing.thing.name
}

output "cert" {
	value = tls_self_signed_cert.cert.cert_pem
}

output "key" {
	value = tls_private_key.key.private_key_pem
	sensitive = true
}