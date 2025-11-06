resource "aws_lb" "app" {
  name = "app-alb"
  load_balancer_type = "application"
  security_groups = [aws_security_group.alb.id]
  subnets = module.vpc.public_subnets
}

resource "aws_lb_target_group" "app" {
  port = 80
  protocol = "HTTP"
  vpc_id = module.vpc.vpc_id
}
