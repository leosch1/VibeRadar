data "aws_route53_zone" "primary" {
  name         = var.domain_name
  private_zone = false
}

resource "aws_route53_record" "frontend" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.frontend.domain_name
    zone_id                = aws_cloudfront_distribution.frontend.hosted_zone_id
    evaluate_target_health = false
  }
}

# MX Record for Improvmx
resource "aws_route53_record" "mx1_improvmx" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.domain_name
  type    = "MX"
  ttl     = 3600
  records = [
    "10 mx1.improvmx.com.",
    "20 mx2.improvmx.com."
  ]
}

# SPF TXT Record for Improvmx
resource "aws_route53_record" "spf_improvmx" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = var.domain_name
  type    = "TXT"
  ttl     = 3600
  records = [
    "v=spf1 include:spf.improvmx.com ~all"
  ]
}
