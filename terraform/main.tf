resource "azurerm_resource_group" "rg" {
  name = "Gymgenius-Shellhacks2024"
  location = "westus2"
}

resource "azurerm_app_service_plan" "rg" {
  name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_app_service" "A-service" {
    name = "Gymgenius"
    location = azurerm_resource_group.rg.location
    resource_group_name = azurerm_resource_group.rg.name
    app_service_plan_id = azurerm_app_service_plan.rg.id
}