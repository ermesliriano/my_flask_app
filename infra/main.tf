# Provider de AWS (usar la región deseada, p. ej. eu-west-1 para Dublín)
provider "aws" {
  region = "eu-west-1"
}

# (Opcional) Obtener la VPC por defecto
data "aws_vpc" "default" {
  default = true
}
data "aws_subnet_ids" "default_subnets" {
  vpc_id = data.aws_vpc.default.id
}

# Grupo de seguridad para Jenkins
resource "aws_security_group" "jenkins_sg" {
  name   = "jenkins-sg"
  vpc_id = data.aws_vpc.default.id

  ingress { from_port = 22, to_port = 22, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }      # SSH abierto (mejor restringir a tu IP en producción)
  ingress { from_port = 8080, to_port = 8080, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }  # Interfaz Jenkins
  ingress { from_port = 80, to_port = 80, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }      # (Opcional) HTTP abierto
  egress  { from_port = 0, to_port = 0, protocol = "-1", cidr_blocks = ["0.0.0.0/0"] }         # Salida abierta

  tags = { Name = "Jenkins-Server-SG" }
}

# Grupo de seguridad para servidor de despliegue
resource "aws_security_group" "deploy_sg" {
  name   = "deployment-sg"
  vpc_id = data.aws_vpc.default.id

  ingress { from_port = 22, to_port = 22, protocol = "tcp", security_groups = [aws_security_group.jenkins_sg.id] }  # SSH desde Jenkins SG
  ingress { from_port = 5432, to_port = 5432, protocol = "tcp", security_groups = [aws_security_group.jenkins_sg.id] }  # PostgreSQL desde Jenkins SG
  ingress { from_port = 80, to_port = 80, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }    # HTTP abierto (para app)
  ingress { from_port = 443, to_port = 443, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }  # HTTPS abierto (futuro, si aplicas SSL)
  egress  { from_port = 0, to_port = 0, protocol = "-1", cidr_blocks = ["0.0.0.0/0"] }

  tags = { Name = "Deployment-Server-SG" }
}

# Crear instancia EC2 para Jenkins Server
resource "aws_instance" "jenkins" {
  ami           = "ami-04b9e92b5572fa0d1"   # <--- ID de AMI (ejemplo: Ubuntu 22.04 en eu-west-1)
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet_ids.default_subnets.ids[0]
  security_groups = [aws_security_group.jenkins_sg.id]
  key_name      = "jenkins-keypair"        # <--- Nombre del Key Pair existente para SSH
  tags = { Name = "Jenkins-Server" }
}

# Crear instancia EC2 para Deployment Server
resource "aws_instance" "deploy" {
  ami           = "ami-04b9e92b5572fa0d1"   # <--- ID de AMI (usar misma región que Jenkins)
  instance_type = "t2.micro"
  subnet_id     = data.aws_subnet_ids.default_subnets.ids[0]
  security_groups = [aws_security_group.deploy_sg.id]
  key_name      = "jenkins-keypair"        # <--- Reutiliza el mismo Key Pair para simplificar acceso
  tags = { Name = "Deployment-Server" }
}
