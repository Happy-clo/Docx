import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Aterial Docs',
  tagline: '希望您在这里度过愉快的时光，收获满满！🎉✨',
  favicon: 'img/favicon.ico',
  onBrokenLinks: 'ignore',
  // Set the production url of your site here
  url: 'https://docs.aterial.top/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Aterial-clo', // Usually your GitHub org/user name.
  projectName: 'plugin-docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: [ 'zh-Hans' ],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: '插件开发指南',
        logo: {
          alt: 'Logo',
          src: 'img/logo.svg',
        },
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: '文档',
            items: [
              {
                href: 'https://docs.aterial.top',
                label: '插件开发指南',
              },
            ],
          },
          {
            title: '关于',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Aterial-Clo',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Aterial Docs, Inc.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
