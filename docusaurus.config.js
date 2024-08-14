import { themes as prismThemes } from 'prism-react-renderer';
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Artaphy Docs',
  tagline: '希望您在这里度过愉快的时光，收获满满！🎉✨',
  favicon: 'img/favicon.ico',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',
  url: 'https://docs.aterial.top',
  baseUrl: '/',
  organizationName: 'Artaphy',
  projectName: 'plugin-docs',
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
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Artaphy Docs',
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
                href: 'https://github.com/Happy-clo/Docx',
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
