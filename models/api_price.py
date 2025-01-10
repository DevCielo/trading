from models.base_api_price import BaseApiPrice


class ApiPrice(BaseApiPrice):

    def __init__(self, api_ob, homeConversions):
        super().__init__(api_ob)

        base_instrument = self.instrument.split('_')[1]
        for hc in homeConversions:
            if hc['currency'] == base_instrument:
                self.sell_conv = float(hc['positionValue'])
                self.buy_conv = float(hc['positionValue'])

    def __repr__(self):
        return f"ApiPrice() {self.instrument} {self.ask} {self.bid} {self.sell_conv:.6f} {self.buy_conv:.6f}"
