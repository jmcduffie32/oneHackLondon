resource "aws_api_gateway_rest_api" "example" {
  name        = "NexmoHackathon"
  description = "API For Nexmo"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  parent_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_resource.proxy.id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.proxy.resource_id}"
  http_method = "${aws_api_gateway_method.proxy.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.rest_api.invoke_arn}"
}

resource "aws_api_gateway_deployment" "example" {
  depends_on = [
    "aws_api_gateway_integration.lambda",
  ]

  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  stage_name  = "test"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.rest_api.arn}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_deployment.example.execution_arn}/*/*"
}

resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id   = "${aws_api_gateway_rest_api.example.id}"
  resource_id   = "${aws_api_gateway_rest_api.example.root_resource_id}"
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
  rest_api_id = "${aws_api_gateway_rest_api.example.id}"
  resource_id = "${aws_api_gateway_method.proxy_root.resource_id}"
  http_method = "${aws_api_gateway_method.proxy_root.http_method}"

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.rest_api.invoke_arn}"
}

resource "aws_lambda_function" "rest_api" {
  filename         = "lambda/rest_api/build/lambda_function.zip"
  source_code_hash = "${base64sha256(file("lambda/rest_api/build/lambda_function.zip"))}"
  function_name    = "nexmo_hackathon_rest"
  role             = "${aws_iam_role.default.arn}"
  handler          = "lambda_function.handler"
  runtime          = "python3.6"

  role = "${aws_iam_role.lambda_exec.arn}"

  environment {
    variables = {
      message_table = "${aws_dynamodb_table.message_table.name}"
      jwt           = "${var.JWT}"
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "nexmo_hackathon_rest"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "api_lambda" {
  name = "terraform_lambda_nexmo_rest"
  role = "${aws_iam_role.lambda_exec.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
		{
			"Effect": "Allow",
			"Action": "dynamodb:*",
			"Resource": "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_dynamodb_table.message_table.id}"
			
		}
    ]
}
EOF
}

resource "aws_dynamodb_table" "message_table" {
  name           = "nexmoHackathonTable"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "user"

  attribute {
    name = "user"
    type = "S"
  }
}
