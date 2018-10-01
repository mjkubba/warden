variable "aws_region" {}

variable "tag_BrIT" {
  default     = ""
  description = "barometer id"
}

variable "tag_DCIO" {
  default     = ""
  description = "dico id"
}

variable "tag_Product_Owner" {
  default     = ""
  description = "product owner"
}

variable "tag_Cost_Center" {
  default     = ""
  description = "cost center for billing"
}

variable "tag_Environment" {
  default     = ""
  description = "Environment"
}

variable "tag_BISO" {
  default     = ""
  description = "The BISO"
}

variable "LoggingBucket" {
  default     = ""
  description = "The Logging bucket name"
}
