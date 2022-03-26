provider "yandex" {
  token     = "${var.yc_token}"
  cloud_id  = "${var.yc_id}"
  folder_id = "${var.yc_folder_id}"
  zone      = "ru-central1-a"
}
resource "yandex_compute_instance" "vm" {
  name = "${var.name}-${count.index}"
  
  count = local.instance_count[terraform.workspace]

  resources {
    cores  = local.vm_cores[terraform.workspace]
    memory = local.vm_memory[terraform.workspace]
  }

  boot_disk {
    initialize_params {
      image_id = "fd83n3uou8m03iq9gavu"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_compute_instance" "vm_for_each" {
  
  lifecycle {
    create_before_destroy = true
  }
  
  for_each = local.instances

  name = each.key

  resources {
    cores  = each.value
    memory = each.value
  }

  boot_disk {
    initialize_params {
      image_id = "fd83n3uou8m03iq9gavu"
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_vpc_network" "network-1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}


locals {
  vm_cores = {
    stage = 1
    prod = 2
  }
  vm_memory = {
    stage = 1
    prod = 2
  }
  instance_count = {
    stage = 1
    prod = 2
  }
  instances = {
    "netology_1" = 1
    "netology_2" = 2
  }
}