export default [
  {
    component: 'CNavItem',
    name: 'Dashboard',
    to: '/dashboard',
    // icon: 'cil-speedometer',
    // badge: { color: 'primary', text: 'NEW' },
  },
  {
    component: 'CNavTitle',
    name: 'Content Management',
  },
  {
    component: 'CNavGroup',
    name: 'Client Dashboard',
    // icon: 'cil-chart-line',
    items: [
      {
        component: 'CNavItem',
        name: 'Overview Page',
        to: '/content/client-dashboard?section=overview',
      },
      {
        component: 'CNavItem',
        name: 'Attack Insights',
        to: '/content/client-dashboard?section=attack-insights',
      },
      {
        component: 'CNavItem',
        name: 'Defense Metrics',
        to: '/content/client-dashboard?section=defense-metrics',
      },
      {
        component: 'CNavItem',
        name: 'System Health',
        to: '/content/client-dashboard?section=system-health',
      },
      {
        component: 'CNavItem',
        name: 'Activity Logs',
        to: '/content/client-dashboard?section=activity-logs',
      },
      {
        component: 'CNavItem',
        name: 'Settings',
        to: '/content/client-dashboard?section=settings',
      },
    ],
  },
  {
    component: 'CNavGroup',
    name: 'Frontend Pages',
    // icon: 'cil-browser',
    items: [
      {
        component: 'CNavGroup',
        name: 'Home Page',
        items: [
          {
            component: 'CNavItem',
            name: 'Hero Section',
            to: '/content/pages?page=home&section=hero',
          },
          {
            component: 'CNavItem',
            name: 'Achievements',
            to: '/content/pages?page=home&section=achievements',
          },
          {
            component: 'CNavItem',
            name: 'Features',
            to: '/content/pages?page=home&section=features',
          },
          {
            component: 'CNavItem',
            name: 'Demo CTA',
            to: '/content/pages?page=home&section=demo',
          },
        ],
      },
      {
        component: 'CNavGroup',
        name: 'About Page',
        items: [
          {
            component: 'CNavItem',
            name: 'Hero Section',
            to: '/content/pages?page=about&section=hero',
          },
          {
            component: 'CNavItem',
            name: 'Mission',
            to: '/content/pages?page=about&section=mission',
          },
          {
            component: 'CNavItem',
            name: 'Vision',
            to: '/content/pages?page=about&section=vision',
          },
          {
            component: 'CNavItem',
            name: 'Company Info',
            to: '/content/pages?page=about&section=company',
          },
          {
            component: 'CNavItem',
            name: 'Values',
            to: '/content/pages?page=about&section=values',
          },
        ],
      },
      {
        component: 'CNavItem',
        name: 'Book Demo',
        to: '/content/pages?page=bookdemo',
      },
      {
        component: 'CNavGroup',
        name: 'Auth Pages',
        items: [
          {
            component: 'CNavItem',
            name: 'Login Page',
            to: '/content/pages?page=auth&section=login',
          },
          {
            component: 'CNavItem',
            name: 'Register Page',
            to: '/content/pages?page=auth&section=register',
          },
        ],
      },
      {
        component: 'CNavItem',
        name: 'Blog Posts',
        to: '/content/blog',
      },
      {
        component: 'CNavItem',
        name: 'Pricing Plans',
        to: '/content/pricing',
      },
    ],
  },
  {
    component: 'CNavGroup',
    name: 'Global Elements',
    // icon: 'cil-layers',
    items: [
      {
        component: 'CNavItem',
        name: 'Header & Navigation',
        to: '/content/website?section=header',
      },
      {
        component: 'CNavItem',
        name: 'Footer',
        to: '/content/website?section=footer',
      },
    ],
  },

  {
    component: 'CNavItem',
    name: 'SEO Management',
    to: '/content/seo',
    // icon: 'cil-search',
  },

  {
    component: 'CNavTitle',
    name: 'Business',
  },
  {
    component: 'CNavItem',
    name: 'Demo Requests',
    to: '/business/demo-requests',
    // icon: 'cil-calendar',
  },
  {
    component: 'CNavItem',
    name: 'Client Companies',
    to: '/business/clients',
    // icon: 'cil-building',
  },
  {
    component: 'CNavTitle',
    name: 'Administration',
  },
  {
    component: 'CNavItem',
    name: 'Admin Users',
    to: '/admin/users',
    // icon: 'cil-user',
  },
  {
    component: 'CNavItem',
    name: 'Settings',
    to: '/admin/settings',
    // icon: 'cil-settings',
  },
]
