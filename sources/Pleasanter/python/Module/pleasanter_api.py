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
                return {
                    "Result": True,
                    "ResponseData": data["Response"]["Data"]
                }

        # タイムアウト
        except requests.exceptions.ConnectTimeout as e:
            return {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Timeout Error"
                }
            }


        # 接続エラー
        except requests.exceptions.ConnectionError as e:
            return {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Connection Error"
                }
            }

        # 想定外エラー
        except Exception as e:
            return {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType":str(type(e)),
                    "Message":"Unexcepted Error"
                }
            }



    def get_columns_in_edit_tab(self, site_id: str) -> dict:
        """Return Dict
        Explain:
            - This function retrieves and processes site information required for using GridColumn in edit tab.
        Args:
        - site_id
        """
        
        # URLを作成
        url = self.pl_addr + "api/items/" + str(site_id) + "/getsite"

        # pleasanter標準のカラムで使用するカラムを指定
        default_cols: list = ['CreatedTime', 'UpdatedTime', "Creator", "Updator"]

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
                # 結果の出力
                return {
                    "Result": True,
                    "ResponseData": {
                        "EditColsList": col_list
                    }
                }

            elif response_dict["ResponseData"]["ReferenceType"] == "Sites":
                # ディレクトリサイトがsite_idとして指定されたらNGを返す
                return {
                    "Result": False,
                    "ErrorMsg": {
                        "ErrorType": "Uncorrect site id.",
                        "Message": "This id is directly site id."
                    }
                }

            else:
                # 想定外のエラー
                return {
                    "Result": False,
                    "ErrorMsg": {
                        "ErrorType": "Unexpected.",
                        "Message": "Successfully response. But Unexpected ReferenceType."
                    }
                }

        # リクエスト送信時のエラー
        else:
            return response_dict

    def get_item_record_by_id_in_site(
            self,
            site_id: str,
            record_id: str,
            grid_columns: Optional[list] = None,
        ) -> dict:
        """return dict(result request and data)
        Args:
        - grid_columns: 
            - True: columns in edit tab
            - False: columns in grid(view) tab
        """
        # site_idとrecord_idに同じ値がセットされた
        if site_id == record_id:

            return  {
                "Result": False,
                "ErrorMsg": {
                    "ErrorType": "The ID is invalid.",
                    "Message": "The same value has been specified for both the record ID and the site ID."
                }
            }
            return result_dict

        # payloadを作成
        payload: dict = self.paylaod
        payload.update({
            "View": {
                # Pleasanter上の表示名で取得
                "ApiDataType": "KeyValues",
                # グリッドカラムの指定
                "GridColumns": grid_columns
            }
        })

        # URLを作成
        url = self.pl_addr + "api/items/" + str(record_id) + "/get"

        # リクエスト実行
        response_dict = self._process_request(
            api_url=url,
            payload=payload
        )

        # レスポンスの処理
        if response_dict['Result']:
            # リストかつリストの要素が1つであればレコードIDが指定されている
            if isinstance(response_dict["ResponseData"], list) and len(response_dict["ResponseData"]) == 1:
                result_dict: dict = {
                    "Result": True,
                    "ResponseData": response_dict["ResponseData"]
                }
                return result_dict

            # リスト以外もしくはレコードIDが複数行ある
            else:
                result_dict: dict = {
                    "Result": False,
                    "ErrorMsg": {
                        "ErrorType": "The provided ID is incorrect.",
                        "Message": "The provided ID is site id or folder id."
                    }
                }
                return result_dict

        else:
            # エディットカラム取得時のリクエストのエラー
            return response_dict





