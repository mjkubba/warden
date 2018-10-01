module "s3_bucket" {
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
