import hcl
import unittest
import sys
import json
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

policy = json.loads("""{
  "tags": ["DCIO", "BrIT", "BISO", "public Access", "Environment", "Cost Center", "Product Owner"],
  "exist" : [{
      "versioning" : {
        "enabled" : true
      }
    }
  ],
  "not-exist" : ["gardening"]
}
""")

combined = ""
with open("tests/test_data/backend.tf", 'r') as fp: combined = combined + fp.read()
with open("tests/test_data/main.tf", 'r') as fp: combined = combined + fp.read()


class wardenTests(unittest.TestCase):
    def test_combine_hcl(self):
        self.assertEqual(warden.combine_hcl("tests/test_data/"), combined)

    def test_get_modules(self):
        self.assertEqual(warden.get_modules(test_mod), [test_mod["module"]["s3_bucket"]["source"]])

    def test_get_resources(self):
        self.assertEqual(warden.get_resources(test_obj), [test_obj["resource"]])

    def test_check_if_allowed_service(self):
        self.assertEqual(warden.check_if_allowed_service([test_obj["resource"]]), True)

    def test_are_objects_equal(self):
        self.assertEqual(warden.are_objects_equal(["a", "b", "c"], ["c", "b", "a"]), True)

    def test_check_tags(self):
        self.assertEqual(warden.check_tags(test_obj["resource"]["aws_s3_bucket"], policy), True)

    def test_check_exist(self):
        self.assertEqual(warden.check_exist(test_obj["resource"]["aws_s3_bucket"], policy), True)

    def test_check_not_exist(self):
        self.assertEqual(warden.check_not_exist(test_obj["resource"]["aws_s3_bucket"], policy), True)

    def test_check_for_policy_complience(self):
        self.assertEqual(warden.check_for_policy_complience("aws_s3_bucket", test_obj["resource"]["aws_s3_bucket"]), True)

    def test_check_policies(self):
        self.assertEqual(warden.check_policies([test_obj["resource"]]), True)

if __name__ == '__main__':
    unittest.main()
