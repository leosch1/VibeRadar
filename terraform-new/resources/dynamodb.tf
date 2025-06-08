resource "aws_dynamodb_table" "vibes" {
  name         = "vibes"
  hash_key     = "id"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "id"
    type = "S"
  }
}
