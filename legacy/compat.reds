// Patch 1.x compat: HandleStorageSlotInput (renamed to HandleStorageSlotClick in 2.0).
// The 2.x equivalent lives in compat.reds and is shipped in the default archive.

@wrapMethod(FullscreenVendorGameController)
private final func HandleStorageSlotInput(evt: ref<ItemDisplayClickEvent>) -> Void {
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
