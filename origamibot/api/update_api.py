from typing import List, Literal, Optional, Union
from io import IOBase

from ._base import APIBase
from .._hints import UpdateTypeStr, URLTypes
from ..types import Update, WebhookInfo


class UpdateAPI(APIBase):
    """An API for handling updates and setting webhooks
    """
    
    def __init__(self, token: str, **params) -> None:
        super().__init__(token, **params)
        
        self.__offset: Optional[int] = 0

        self.__limit: Optional[int] = \
            params.get('update_limit', None)
        
        self.__timeout: Optional[int] = \
            params.get('update_timeout', None)
        
        self.__allowed_updates: Optional[List[UpdateTypeStr]] = \
            params.get('allowed_updates', None)

    async def get_updates(self,
                          offset: Optional[int] = None,
                          limit: Optional[int] = None,
                          timeout: Optional[int] = None,
                          allowed_updates: Optional[List[UpdateTypeStr]] = None
                          ) -> List[Update]:
        """Get incoming updates from the server.
        
        Returns list of Update objects.
        
        :param offset: Identifier of the first update to be returned.
            Must be greater by one than the highest among the identifiers
            of previously received updates.
        :param limit: Limits the number of updates to be retrieved.
            Values between 1-100 are accepted.
        :param timeout: Timeout in seconds for long polling. Defaults to 0,
            i.e. usual short polling. Should be positive, short polling
            should be used for testing purposes only.
        :param allowed_updates: A JSON-serialized list of the update
            types you want your bot to receive.
        """
        data = dict(
            offset = offset or self.__offset,
            limit = limit or self.__limit,
            timeout = timeout or self.__timeout,
            allowed_updates = allowed_updates or self.__allowed_updates
        )
        
        response = await self._send_request('getUpdates', data=data)
        assert isinstance(response, dict)
        
        result = self._extract_request_result(response)
        assert isinstance(result, list)
        
        return [Update.construct(**i) for i in result]
    
    async def set_webhook(self,
                          url: URLTypes,
                          certificate: Optional[Union[IOBase, str]] = None,
                          ip_address: Optional[str] = None,
                          max_connections: Optional[int] = None,
                          allowed_updates: Optional[List[UpdateTypeStr]] = None,
                          drop_pending_updates: Optional[bool] = None
                          ) -> Literal[True]:
        """Use this method to specify a url and receive incoming
        updates via an outgoing webhook.
        
        Whenever there is an update
        for the bot, we will send an HTTPS POST request to the specified
        url, containing a JSON-serialized Update.
 
        :param url: HTTPS url to send updates to. Use an empty string to
            remove webhook integration
        :param certificate: Upload your public key certificate so that
            the root certificate in use can be checked. See our
            self-signed guide for details.
        :param ip_address: The fixed IP address which will be used to
            send webhook requests instead of the IP address resolved
            through DNS
        :param max_connections: Maximum allowed number of simultaneous HTTPS
            connections to the webhook for update delivery, 1-100.
            Defaults to 40.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive.
        :param drop_pending_updates: Pass True to drop all pending updates
        """
        data = dict(
            url = url,
            ip_address = ip_address,
            max_connections = max_connections,
            allowed_updates = allowed_updates,
            drop_pending_updates = drop_pending_updates
        )

        if isinstance(certificate, IOBase):
            files = {'certificate': certificate}
        else:
            files = None
            data['certificate'] = certificate

        return self._extract_request_result(
            await self._send_request(
                'setWebhook',
                data=data,
                files=files
                )
            )
    
    async def delete_webhook(self,
                             drop_pending_updates: Optional[bool] = None
                             ) -> Literal[True]:
        """Use this method to remove webhook integration.
        
        Returns True on success.
        
        :param drop_pending_updates: Pass True to drop all pending updates
        """
        return self._extract_request_result(
            await self._send_request(
                'deleteWebhook',
                data={'drop_pending_updates': drop_pending_updates}
            )
        )

    async def get_webhook_info(self) -> WebhookInfo:
        """Use this method to get current webhook status.
        
        Requires no parameters.
        
        On success, returns a WebhookInfo object.
        
        If the bot is using getUpdates, will return
        an object with the url field empty.
        """
        return WebhookInfo.construct(
            **self._extract_request_result(
                await self._send_request('getWebhookInfo')
            )
        )
    