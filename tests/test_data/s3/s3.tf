resource "aws_s3_bucket" "test-bucket" {
  bucket = "${var.tag_DCIO}-mj-test-${var.environment}-${var.function}"
  acl    = "private"
  logging {
    # we can use data to get the logging bucket too
    target_bucket = "${var.LoggingBucket}"
    target_prefix = "logs/"
  }

  versioning {
    enabled = true
  }
  # gardening { "maybe" = true }
  tags {
    BrIT            = "${var.tag_BrIT}"
    DCIO            = "${var.tag_DCIO}"
    "Product Owner" = "${var.tag_Product_Owner}"
    "Cost Center"   = "${var.tag_Cost_Center}"
    Environment     = "${var.tag_Environment}"
    "public Access" = "NO"
    BISO            = "${var.tag_BISO}"
  }
}
