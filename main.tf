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
  shared_credentials_files = ["key/aws_credentials.ini"]
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
resource "aws_iot_thing_type" "raspberry_pi" {
  name = "RaspberryPi"
}

resource "aws_iot_thing" "raspi" {
  name       = "Raspi"
  thing_type_name = aws_iot_thing_type.raspberry_pi.name
}

resource "aws_iot_policy" "raspi_policy" {
  name = "RaspberryPiPolicy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:*",
      "Resource": "*"
    }
  ]
}
EOF
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
  thing     = aws_iot_thing.raspi.name
}

resource "local_file" "cert" {
  content  = tls_self_signed_cert.cert.cert_pem
  filename = "${path.module}/IoT_certificate.pem.crt"
}


resource "local_file" "private_key" {
  content  = tls_private_key.key.private_key_pem
  filename = "${path.module}/IoT_private_key.pem"
}

data "http" "root_ca" {
  url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
}

resource "local_file" "IoT_root_ca" {
  content  = data.http.root_ca.response_body
  filename = "${path.module}/rootCA.pem"
}
