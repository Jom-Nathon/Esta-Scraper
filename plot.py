class Plot:
    def __init__(self, lotNumber, saleOrder, ID, type, size, estimatedPrice, subDistrict, district, province) -> None:
        self.lotNumber = lotNumber
        self.saleOrder = saleOrder
        self.ID = ID
        self.type = type
        self.size = size
        self.estimatedPrice = estimatedPrice
        #sub district = tambon
        self.subDistrict = subDistrict
        #district = amphur
        self.district = district
        self.province = province

    def __str__(self):
        return self.ID + ', ' + self.type + ', ' + self.estimatedPrice + '\n'