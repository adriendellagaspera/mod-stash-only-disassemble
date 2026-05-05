// Patch 2.0+ compat: HandleStorageSlotClick (renamed from HandleStorageSlotInput in 1.x).
// The 1.x equivalent lives in legacy/compat.reds and is shipped in the legacy archive.

@wrapMethod(FullscreenVendorGameController)
private final func HandleStorageSlotClick(evt: ref<ItemDisplayClickEvent>) -> Void {
    wrappedMethod(evt);

    if this.IsStashMode() && evt.actionName.IsAction(DisassemblePolicy.ActionName()) && IsDefined(evt.uiInventoryItem) {
        let item = evt.uiInventoryItem.GetItemData();
        if DisassemblePolicy.IsItemDisassemblable(item) {
            let qty = item.GetQuantity();
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
