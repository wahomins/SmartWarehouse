// material icon
import AddIcon from '@material-ui/icons/Add';
import DevicesIcon from '@material-ui/icons/DeviceHub';
import ViewListIcon from '@material-ui/icons/ViewList';
import PeopleIcon from '@material-ui/icons/People';
import CollectionIcon from '@material-ui/icons/Collections';
import SportsEsportsIcon from '@material-ui/icons/SportsEsports';
import DashboardIcon from '@material-ui/icons/Dashboard';
import AssessmentIcon from '@material-ui/icons/Assessment';

// configs
import { PATH_NAME, DRAWER_MENU_LABEL } from 'configs';

export const navBarCommon = [
  {
    subheader: 'Application',
    items: [
      {
        title: 'Report',
        href: PATH_NAME.DASHBOARD,
        icon: DashboardIcon,
        label: DRAWER_MENU_LABEL.DASHBOARD,
      },
      // {
      //   title: 'Playbackground',
      //   href: PATH_NAME.PLAY_BACKGROUND,
      //   icon: SportsEsportsIcon,
      //   label: DRAWER_MENU_LABEL.PLAY_BACKGROUND,
      // },
    ],
  },
  {
    subheader: 'Dashboard',
    items: [
      {
        title: 'Device',
        icon: DevicesIcon,
        href: PATH_NAME.DEVICE,
        label: DRAWER_MENU_LABEL.DEVICE,
        items: [
          {
            title: 'Add Device',
            icon: AddIcon,
            href: PATH_NAME.DEVICE_ADD,
            label: DRAWER_MENU_LABEL.DEVICE_ADD,
          },
          {
            title: 'List Devices',
            icon: ViewListIcon,
            href: PATH_NAME.DEVICE_LIST,
            label: DRAWER_MENU_LABEL.DEVICE_LIST,
          },
          {
            title: 'Devices Log',
            icon: ViewListIcon,
            href: PATH_NAME.DEVICE_LOGS,
            label: DRAWER_MENU_LABEL.DEVICE_LOGS,
          },
        ],
      },
      {
        title: 'Warehouse',
        icon: AssessmentIcon,
        href: PATH_NAME.WAREHOUSE_LIST,
        label: DRAWER_MENU_LABEL.WAREHOUSE,
        items: [
          {
            title: 'Add Warehouse',
            icon: AddIcon,
            href: PATH_NAME.WAREHOUSE_ADD,
            label: DRAWER_MENU_LABEL.WAREHOUSE_ADD,
          },
          {
            title: 'List Warehouses',
            icon: ViewListIcon,
            href: PATH_NAME.WAREHOUSE_LIST,
            label: DRAWER_MENU_LABEL.WAREHOUSE_LIST,
          },
        ],
      },
      {
        title: 'Users',
        icon: PeopleIcon,
        href: PATH_NAME.USERS,
        label: DRAWER_MENU_LABEL.USERS,
        items: [
          {
            title: 'Users',
            icon: ViewListIcon,
            href: PATH_NAME.USERS_LIST,
            label: DRAWER_MENU_LABEL.LIST,
          },
          {
            title: 'AccessLogs',
            icon: CollectionIcon,
            href: PATH_NAME.USERS_ACCESS_LOGS,
            label: DRAWER_MENU_LABEL.ACCESSLOGS,
          },
        ],
      },
      // {
      //   title: 'Kanban',
      //   href: PATH_NAME.KANBAN,
      //   icon: AssessmentIcon,
      //   label: DRAWER_MENU_LABEL.KANBAN,
      // },
    ],
  },
  {
    // subheader: 'Users',
    // icon: PeopleIcon,
    // href: PATH_NAME.USERS,
    // label: DRAWER_MENU_LABEL.USERS,
    // items: [
    //   {
    //     title: 'Users',
    //     icon: ViewListIcon,
    //     href: PATH_NAME.USERS_LIST,
    //     label: DRAWER_MENU_LABEL.LIST,
    //   },
    //   {
    //     title: 'AccessLogs',
    //     icon: CollectionIcon,
    //     href: PATH_NAME.USERS_ACCESS_LOGS,
    //     label: DRAWER_MENU_LABEL.ACCESSLOGS,
    //   },
    // ],
  },
];
