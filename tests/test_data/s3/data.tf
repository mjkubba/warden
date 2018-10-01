data "aws_s3_bucket" "s3_bucket_logs" {
  filter{
    name   = "tag:Name"
    values = ["*access-logs*"]
  }
  hosted_zone_id = "us-east-1"
}
