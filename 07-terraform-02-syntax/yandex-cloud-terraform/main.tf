terraform {
  required_providers {
    yandex = {
      source = "terraform-registry.storage.yandexcloud.net/yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  token     = "${var.yc_token}"
  cloud_id  = "${var.yc_id}"
  folder_id = "${var.yc_folder_id}"
  zone      = "ru-central1-a"
}