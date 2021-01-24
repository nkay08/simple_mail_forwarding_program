from credentials import Credentials
from enums import MailStatus, FetchProtocol
from base import ConfigObject


class ForwardingRule(ConfigObject):

    def __init__(self,
                 from_address: str,
                 to_address: str,
                 credentials: Credentials,
                 credentials_outgoing: Credentials,
                 status: MailStatus = MailStatus.UNREAD,
                 folder: str = 'INBOX',
                 protocol: FetchProtocol = FetchProtocol.IMAP,
                 name: str = "",
                 save_ids: bool = True,
                 schedule: int = 1800 # Half an hour
                 ) -> 'ForwardingRule':
        if not from_address:
            raise Exception("No FROM address specified")
        self._from_address = from_address

        if not to_address:
            raise Exception("No TO address specified")
        self._to_address = to_address

        if not credentials:
            raise Exception("No credentials specified")
        self._credentials = credentials

        if not credentials_outgoing:
            raise Exception("No credentials specified")
        self._credentials_outgoing = credentials_outgoing

        if not status:
            raise Exception("No status condition. Default is UNREAD.")
        self._status = status

        if not folder:
            raise Exception("No folder specified. Default is INBOX.")
        self._folder = folder

        if not protocol:
            raise Exception("No protocol specified. Default is IMAP.")
        self._protocol = protocol

        if not name:
            self.name = self._credentials.host

        self._save_ids = save_ids
        self._schedule = schedule

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__class__.__name__ + "::" + self.name
    
    @property
    def from_address(self) -> str:
        return self._from_address

    @from_address.setter
    def from_address(self, from_address: str):
        self._from_address = from_address

    @property
    def to_address(self) -> str:
        return self._to_address

    @to_address.setter
    def to_address(self, to_address: str):
        self._to_address = to_address

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: Credentials):
        self._credentials = credentials

    @property
    def credentials_outgoing(self) -> Credentials:
        return self._credentials_outgoing

    @credentials_outgoing.setter
    def credentials_outgoing(self, credentials: Credentials):
        self._credentials_outgoing = credentials_outgoing

    @property
    def folder(self) -> str:
        return self._folder

    @folder.setter
    def folder(self, folder: str):
        self._folder = folder

    @property
    def status(self) -> MailStatus:
        return self._status

    @status.setter
    def status(self, status: MailStatus):
        self._status = status

    @property
    def protocol(self) -> FetchProtocol:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: FetchProtocol):
        self._protocol = protocol

    @property
    def schedule(self) -> int:
        return self._schedule

    @schedule.setter
    def schedule(self, schedule: int):
        self._schedule = schedule

    @property
    def save_ids(self) -> bool:
        return self._save_ids


    def _from_json(json_dict: dict) -> 'Email':
        # if not json_dict.get('credentials', False):
        #     raise Exception("No credentials specified for rule.")

        if json_dict.get('credentials', False):
            # Load credentials from nested json
            creds_raw = json_dict.get('credentials')

            if creds_raw.get('incoming', False):
                creds_incoming_raw = creds_raw.get('incoming')
                if type(creds_incoming_raw) is dict:
                    # if credentials is dict, load it
                    creds_incoming = Credentials.from_json(creds_incoming_raw)
                elif type(creds_incoming_raw) is str:
                    # if credentials is str, load from file
                    creds = Credentials.from_json_file(creds_incoming_raw)
                else:
                    raise Exception("Credentials not in a suitable format")
            else:
                raise Exception("No credentials for incoming mails")

            if creds_raw.get('outgoing', False):
                creds_outgoing_raw = creds_raw.get('outgoing')
                if type(creds_outgoing_raw) is dict:
                    # if credentials is dict, load it
                    creds_outgoing = Credentials.from_json(creds_outgoing_raw)
                elif type(creds_outgoing_raw) is str:
                    # if credentials is str, load from file
                    creds_outgoing = Credentials.from_json_file(creds_outgoing_raw)
                else:
                    raise Exception("Credentials not in a suitable format")
            else:
                raise Exception("No credentials for incoming mails")
        else:
            # Legacy
            # # Load credentials directly from non-nested json
            # creds = Credentials.from_json(json_dict)
            raise Exception("No credentials")

        kwargs: dict = {'credentials': creds_incoming, 'credentials_outgoing': creds_outgoing}
        args = []

        if json_dict.get('from_address', False):
            args.append(json_dict.get('from_address'))
        if json_dict.get('to_address', False):
            args.append(json_dict.get('to_address'))
        if json_dict.get('status', False):
            kwargs['status'] = json_dict.get('status')
        if json_dict.get('folder', False):
            kwargs['folder'] = json_dict.get('folder')
        if json_dict.get('protocol', False):
            kwargs['protocol'] = json_dict.get('protocol')
        if json_dict.get('name', False):
            kwargs['name'] = json_dict.get('name')
        if json_dict.get('save_ids', False):
            kwargs['save_ids'] = json_dict.get('save_ids')
        if json_dict.get('schedule', False):
            kwargs['schedule'] = json_dict.get('schedule')

        return ForwardingRule(*args, **kwargs)

    @classmethod
    def from_json_file(cls, filepath: str) -> 'ForwardingRule':
        obj: ForwardingRule = super().from_json_file(filepath)

        from pathlib import Path
        obj.name = Path(filepath).stem

        return obj
