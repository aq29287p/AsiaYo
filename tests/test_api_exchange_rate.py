from requests import Response
from ast import literal_eval
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiExchangeRate(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_200_when_happy_case(self):
        """Happy case，應該回應200"""
        test_data= {
            "source": "USD",
            "target": "JPY",
            "amount": "$1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(200, res.status_code)
            res_data=literal_eval(res.data.decode('utf-8'))
            self.assertEqual("$170,496.53", res_data['amount'])

    def test_it_should_404_when_url_is_wrong(self):
        """wrong url，應該回應404"""
        test_data= {
            "source": "USD",
            "target": "JPY",
            "amount": "$1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate-123",query_string=test_data)
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_lack_of_source_parameter(self):
        """少source參數，應該回應400"""
        test_data= {
            "target": "JPY",
            "amount": "$1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(400, res.status_code)

    def test_it_should_400_when_lack_of_target_parameter(self):
        """少target參數，應該回應400"""
        test_data= {
            "source": "JPY",
            "amount": "$1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(400, res.status_code)

    def test_it_should_422_when_amount_lack_of_dollar_sign(self):
        """金額格式錯誤，缺$符號，應該回應422"""
        test_data= {
            "source": "USD",
            "target": "JPY",
            "amount": "1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(422, res.status_code)
            res_data=literal_eval(res.data.decode('utf-8'))
            self.assertEqual('amount 應以 $ 開頭 例如 $12.45', res_data['message'])

    def test_it_should_422_when_amount_is_not_a_number(self):
        """金額格式錯誤，$後應為數字，應該回應422"""
        test_data= {
            "source": "USD",
            "target": "JPY",
            "amount": "$abc"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(422, res.status_code)
            res_data=literal_eval(res.data.decode('utf-8'))
            self.assertEqual('amount 應以 $後面應為數字 例如 $12.45', res_data['message'])

    def test_it_should_409_when_currency_is_not_supported(self):
        """貨幣不支援，應該回應409"""
        test_data= {
            "source": "CAD",
            "target": "JPY",
            "amount": "$1,525"
        }
        with self.app.test_client() as client:
            res: Response = client.get("/exchange-rate",query_string=test_data)
            self.assertEqual(409, res.status_code)
            res_data=literal_eval(res.data.decode('utf-8'))
            self.assertEqual('CAD is not support', res_data['message'])