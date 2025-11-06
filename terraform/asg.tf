data "aws_ami" "windows" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["Windows_Server-2019-English-Full-Base-*"]
  }
}

resource "aws_launch_template" "app" {
  name = "app-lt-${random_id.id.hex}"
  image_id = data.aws_ami.windows.id
  instance_type = var.instance_type
  user_data = base64encode(file("../scripts/user-data.ps1"))

  network_interfaces {
    associate_public_ip_address = false
    security_groups = [aws_security_group.app.id]
  }
}

resource "aws_autoscaling_group" "app" {
  name = var.asg_name
  launch_template {
    id = aws_launch_template.app.id
    version = "$Latest"
  }
  min_size = 1
  max_size = 3
  vpc_zone_identifier = module.vpc.private_subnets
}
