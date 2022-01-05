{
    'name': "Mstech Timajas",
    "category": "External Service",
    'author': "Meditech",
    'summary':"Mstech External Service - Timajas",
    'depends': [
        'sale',
        'stock',
        'industry_fsm',
        'industry_fsm_sale',

    ],
    'data': [
        'data/project_data.xml',
        'views/view_project_task.xml',
    ],
    'installable' : True,
    'auto_install' :  False,
    'application' :  False,
}
