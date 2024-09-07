from datetime import datetime

from baked.lib.admin.model.userpermission import UserPermission
from baked.lib.admin.service.accountservice import AccountService
from baked.lib.admin.service.credentialservice import CredentialService
from baked.lib.admin.service.permissionservice import PermissionService
from baked.lib.admin.service.userservice import UserService

from baked.lib.protected.protected import encrypt, hash_string
from baked.lib.setup.abstractsetup import AbstractSetup
from baked.lib.wedding.model.admin import Account, User, UserData


class WeddingSetup(AbstractSetup):
    """Setup Wedding Backend."""

    def setup(self):
        # encryption key
        cred_service = CredentialService()
        key = cred_service.get_key()
        if not key:
            key = CredentialService().create_key()

        account_service = AccountService("wedding")
        aid = len(account_service.list()) + 1
        admin_account = Account(id=aid, account_id="admin")
        public_account = Account(id=aid + 1, account_id="guests")

        for account in [admin_account, public_account]:
            # ensure admin doesn't already exist
            try:
                account_service.get(account_id=account.account_id)

                raise EnvironmentError(f"{account.account_id} already exists.")

            except ValueError:
                account_service.create(account)

        # add root user
        # TODO: This should be moved to the abstract for every application.
        user_service = UserService("wedding")
        permission_service = PermissionService()

        uid = len(user_service.list()) + 1

        user_data = UserData(key=key,
                             pwd_hash=encrypt(key, hash_string("ashley&martin14E17!")),
                             pwd_last_updated=datetime.now())

        user = User(id=uid, account="admin", firstname="martin", lastname="baker", email="baker.bsc@gmail.com", user_id="baker.bsc@gmail.com", data=user_data)
        
        permission = UserPermission(name="SYSTEMADMIN", type="switch", permission="1")
        permission_service.set_user_permission(user, permission)

        permission = UserPermission(name="USERADMIN", type="switch", permission="1")
        permission_service.set_user_permission(user, permission)
        
        user_service.create(user)

    def get_admin_user_id(self):
        return "user_id", "baker.bsc@gmail.com"
