import hcl
import unittest
import sys
sys.path.append("../.")
import warden

test_obj = hcl.loads("""resource "aws_s3_bucket" "test-bucket" {
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

  tags {
    BrIT            = "${var.tag_BrIT}"
    DCIO            = "${var.tag_DCIO}"
    "Product Owner" = "${var.tag_Product_Owner}"
    "Cost Center"   = "${var.tag_Cost_Center}"
    Environment     = "${var.tag_Environment}"
    "public Access" = "NO"
    BISO            = "${var.tag_BISO}"
  }
}""")

test_mod = hcl.loads("""module "s3_bucket" {
 source = "s3/"
 aws_region = "${var.aws_region}"
 "function"                    = "${var.LoggingBucket}"
 "function"                    = "${var.function}"
 "tag_BrIT"                    = "${var.tag_BrIT}"
 "tag_Cost_Center"             = "${var.tag_Cost_Center}"
 "tag_DCIO"                    = "${var.tag_DCIO}"
 "tag_Environment"             = "${var.tag_Environment}"
 "tag_Product_Owner"           = "${var.tag_Product_Owner}"
 "tag_BISO"                    = "${var.BISO}"
}
 """)

combined = ""
with open("tests/test_data/backend.tf", 'r') as fp: combined = combined + fp.read()
with open("tests/test_data/main.tf", 'r') as fp: combined = combined + fp.read()

class wardenTests(unittest.TestCase):
    def test_get_resources(self):
        self.assertEqual(warden.get_resources(test_obj), [test_obj["resource"]])

    def test_get_modules(self):
        self.assertEqual(warden.get_modules(test_mod), [test_mod["module"]["s3_bucket"]["source"]])

    def test_combine_hcl(self):
        self.assertEqual(warden.combine_hcl("tests/test_data/"), combined)


if __name__ == '__main__':
    unittest.main()
