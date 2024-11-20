import json
import requests
from typing import Optional,Tuple


class PleasanterConnector:
    def __init__(self, pl_addr: str , api_key: str) -> None:
        self.pl_addr: str = pl_addr
        self.api_key: str = api_key
        self.timeout: tuple = (3.0, 10.0)
        self.paylaod: dict = {
            "ApiVersion": 1.1,
            "apiKey": self.api_key,
        }

    def _handle_http_error(self, status_code: int) -> dict:
        """Handle non-200 HTTP status codes"""
        return {
            "Result": False,
            "ErrorMsg": {
                "ErrorType": str(status_code),
                "Message": "HTTP Request Error"
            }
        }



    def _process_request(self, api_url:str, payload:dict) -> dict:
        """Common process request to pleasanter api"""
        try:
            # APIにリクエストを送信
            request_post = requests.post(
                api_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json', 'charset': 'UTF-8'},
                timeout=self.timeout
            )

            # HTTPレスポンスの判定
            if request_post.status_code != 200:
                # 200以外のレスポンス
                return self._handle_http_error(request_post.status_code)

            else:
                # レスポンスをjson形式に変換
                data: dict = request_post.json()
                # 返り値を作成
                response_dict: dict = {
                    "Result": True,
                    "ResponseData": data["Response"]["Data"]
                }
                return response_dict

        # タイムアウト
        except requests.exceptions.ConnectTimeout as e:
            error_msg: dict = {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Timeout Error"
                }
            }

            return error_msg

        # 接続エラー
        except requests.exceptions.ConnectionError as e:
            error_msg: dict = {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Connection Error"
                }
            }
            return error_msg

        # 想定外エラー
        except Exception as e:
            error_msg: dict = {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Unexcepted Error"
                }
            }
            return error_msg



    def _get_columns_in_edit_tab(self, site_id: str) -> dict:
        """Return Dict
        Explain:
            - This function retrieves and processes site information required for using GridColumn in edit tab.
        Args:
        - site_id
        """
        
        # URLを作成
        url = self.pl_addr + "api/items/" + str(site_id) + "/getsite"

        # pleasanter標準のカラムで使用するカラムを指定
        default_cols: list = ['CreatedTime', 'UpdatedTime']

        # try:
        # APIにリクエストするデータを作成
        payload: dict = self.paylaod

        response_dict = self._process_request(
            api_url=url,
            payload=payload
        )

        # リクエストの判定
        if response_dict["Result"]:
            # 対象IDがサイトかどうかの確認
            if response_dict["ResponseData"]["ReferenceType"] in ["Results", "Issues"]:
                # エディットタブで使用されているカラムを取得
                col_list: list = response_dict["ResponseData"]["SiteSettings"]["EditorColumnHash"]["General"]
                # デフォルトカラムで使用するカラム名を追加
                col_list.extend(default_cols)

                result_dict: dict = {
                    "Result": True,
                    "Data": {
                        "EditColsList": col_list
                    }
                }

                return result_dict


            elif response_dict["ResponseData"]["ReferenceType"] == "Sites":
                # ディレクトリサイトがsite_idとして指定されたらNGを返す
                result_dict: dict = {
                    "Result": False,
                    "ErrorMsg": {
                        "ErrorType": "Uncorrect site id.",
                        "Message": "This id is directly site id."
                    }
                }
                return result_dict

            else:
                # 想定外のエラー
                result_dict: dict = {
                    "Result": False,
                    "ErrorMsg": {
                        "ErrorType": "Unexpected.",
                        "Message": "Successfully response. But Unexpected ReferenceType."
                    }
                }
                return result_dict

        # リクエスト送信時のエラー
        else:
            return response_dict