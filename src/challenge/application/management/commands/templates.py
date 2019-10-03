APP_INFO = (
    f'  ID...........: {{app_id}}\n'
    f'  NAME.........: {{name}}\n'
    f'  CLIENT_ID....: {{client_id}}\n'
    f'  CLIENT_SECRET: {{client_secret}}\n'
    f'  ACTIVE.......: {{is_active}}\n'
    f'  TOKEN........: {{token}}\n'
)

NEW_APP_INFO = f'NEW APPLICATION\n{APP_INFO}'

APP_PAGE_INFO = f'-- You are on page {{page}} --\n'

APP_QUERY_INFO = (
    f'Applications Count: {{count}}\n'
    f'Total Pages: {{num_pages}}\n'
)

TEXT_YES = 'YES'
TEXT_NO = 'NO'

SEPARATOR = '{separator}\n'.format(separator='=' * 80)
