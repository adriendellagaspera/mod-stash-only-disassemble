// Disables disassembly in the backpack; only allows it from the stash.

// --- Block disassembly in the regular backpack ---

@wrapMethod(InventoryGameController)
protected func HandleItemClick(evt: ref<ItemDisplayClickEvent>) -> Void {
    if evt.actionName.IsAction(n"disassemble_item") {
        return;
    }
    wrappedMethod(evt);
}

@wrapMethod(InventoryGameController)
protected cb func OnInventoryItemHoverOver(evt: ref<ItemDisplayHoverOverEvent>) -> Bool {
    let result = wrappedMethod(evt);
    this.m_buttonHintsController.RemoveButtonHint(n"disassemble_item");
    return result;
}

// --- Enable disassembly from the stash ---

@wrapMethod(FullscreenVendorGameController)
private final func HandleStorageSlotClick(evt: ref<ItemDisplayClickEvent>) -> Void {
    wrappedMethod(evt);

    if this.IsStashMode() && evt.actionName.IsAction(n"disassemble_item") && IsDefined(evt.uiInventoryItem) {
        let item = evt.uiInventoryItem.GetItemData();
        let qty = item.GetQuantity();
        if this.CanDisassemble(item) && qty > 0 {
            if evt.uiInventoryItem.IsIconic() {
                this.OpenConfirmationPopup(evt.uiInventoryItem, qty, QuantityPickerActionType.Disassembly, VendorConfirmationPopupType.DisassembeIconic);
            } else if qty > 1 {
                this.OpenQuantityPicker(evt.uiInventoryItem, QuantityPickerActionType.Disassembly);
            } else {
                this.TryDisassembleFromStash(item, 1);
            }
        }
    }
}

@wrapMethod(FullscreenVendorGameController)
protected func OnConfirmationPopupClosed(data: ref<inkGameNotificationData>) -> Bool {
    let handled = wrappedMethod(data);

    if IsDefined(data) {
        let resultData = data as VendorConfirmationPopupCloseData;
        if Equals(resultData.confirm, true) && Equals(resultData.type, VendorConfirmationPopupType.DisassembeIconic) && this.IsStashMode() && IsDefined(resultData.inventoryItem) && resultData.inventoryItem.IsIconic() {
            this.TryDisassembleFromStash(resultData.inventoryItem.GetItemData(), resultData.quantity);
            handled = true;
        }
    }
    return handled;
}

@wrapMethod(FullscreenVendorGameController)
protected func OnQuantityPickerPopupClosed(data: ref<inkGameNotificationData>) -> Bool {
    let handled = wrappedMethod(data);

    if IsDefined(data) {
        let resultData = data as QuantityPickerPopupCloseData;
        if Equals(resultData.actionType, QuantityPickerActionType.Disassembly) && this.IsStashMode() && IsDefined(resultData.inventoryItem) && resultData.choosenQuantity > 0 {
            this.TryDisassembleFromStash(resultData.inventoryItem.GetItemData(), resultData.choosenQuantity);
            handled = true;
        }
    }
    return handled;
}

@wrapMethod(FullscreenVendorGameController)
protected cb func OnInventoryItemHoverOver(evt: ref<ItemDisplayHoverOverEvent>) -> Bool {
    let controller: ref<DropdownListController> = inkWidgetRef.GetController(this.m_sortingDropdown) as DropdownListController;
    let buttonHint = StringToName(GetLocalizedText("LocKey#6887"));
    if !controller.IsOpened() && this.IsStashMode() {
        if evt.uiInventoryItem != null && this.CanDisassemble(evt.uiInventoryItem.GetItemData()) {
            this.m_buttonHintsController.AddButtonHint(n"disassemble_item", buttonHint, true);
        };
    };
    wrappedMethod(evt);
}

@wrapMethod(FullscreenVendorGameController)
protected cb func OnInventoryItemHoverOut(evt: ref<ItemDisplayHoverOutEvent>) -> Bool {
    wrappedMethod(evt);
    this.m_buttonHintsController.RemoveButtonHint(n"disassemble_item");
}

@addMethod(FullscreenVendorGameController)
private func IsStashMode() -> Bool = (!IsDefined(this.m_vendorUserData) && IsDefined(this.m_storageUserData));

@addMethod(FullscreenVendorGameController)
private func CanDisassemble(item: wref<gameItemData>) -> Bool {
    return IsDefined(ItemActionsHelper.GetDisassembleAction(item.GetID()))
        && item.GetQuantity() > 0;
}

@addMethod(FullscreenVendorGameController)
private func TryDisassembleFromStash(item: wref<gameItemData>, qty: Int32) -> Void {
    let player = this.GetPlayerControlledObject();
    ItemActionsHelper.DisassembleItem(player, item.GetID(), qty);
    GameInstance.GetAudioSystem(player.GetGame()).Play(n"ui_menu_item_disassemble");
    this.Update();
}
