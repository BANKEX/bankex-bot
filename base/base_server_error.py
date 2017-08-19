from tornkts.base.server_response import ServerResponseStatus, ServerError


class BankExServerError(ServerError):
    ALREADY_EXIST = ServerResponseStatus('already_exist', 'Entity already exist', 400)
