import { defineConfig } from 'vitepress'
import { fileURLToPath } from 'node:url'
import { dirname, resolve, join } from 'node:path'
import fs from 'node:fs'

const __dirname = dirname(fileURLToPath(import.meta.url))
const docsDir = resolve(__dirname, '..')
const chaptersDir = join(docsDir, 'chapters')
const referenceDir = join(docsDir, 'reference')

function titleOf(file: string): string {
  const txt = fs.readFileSync(file, 'utf-8')
  const m = txt.match(/^#\s+(.+)$/m)
  return m ? m[1].trim() : ''
}

// strip zero-padding: "第 01 章" -> "第 1 章"
function shortTitle(file: string): string {
  return titleOf(file).replace(/^第\s*0?(\d+)\s*章\s*/, '第 $1 章 ')
}

// 4 parts -> chapter numbers (per 《Mapcn 从入门到进阶》大纲)
const parts = [
  { text: '第一部分 入门与环境', items: [1, 2] },
  { text: '第二部分 地图基础与交互', items: [3, 4, 5, 6] },
  { text: '第三部分 图形与数据', items: [7, 8, 9, 10] },
  { text: '第四部分 进阶与实战', items: [11, 12, 13, 14] },
]

const bookSidebar = parts.map((p) => ({
  text: p.text,
  collapsed: false,
  items: p.items.map((n) => ({
    text: shortTitle(join(chaptersDir, `chapter${String(n).padStart(2, '0')}.md`)),
    link: `/chapters/chapter${String(n).padStart(2, '0')}`,
  })),
}))

const refItems = fs
  .readdirSync(referenceDir)
  .filter((f) => f.endsWith('.md'))
  .sort()
  .map((f) => ({
    text: titleOf(join(referenceDir, f)),
    link: `/reference/${f.replace(/\.md$/, '')}`,
  }))

const sidebar = [
  {
    text: '开始阅读',
    items: [
      { text: '前言', link: '/preface' },
      { text: '下载与资源', link: '/downloads' },
    ],
  },
  ...bookSidebar,
  { text: '参考资料（官方文档研读）', items: refItems },
]

const refNav = refItems.map((r) => ({ text: r.text, link: r.link }))

export default defineConfig({
  base: '/mapcn-book/',
  lang: 'zh-CN',
  title: 'Mapcn 从入门到进阶',
  description:
    '基于 mapcn 官方文档的系统性实战指南：构建于 MapLibre GL 之上的 React 地图组件库，从入门到进阶。',
  lastUpdated: true,
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '前言', link: '/preface' },
      { text: '分章阅读', link: '/chapters/chapter01' },
      { text: '参考资料', items: refNav },
      { text: '下载', link: '/downloads' },
    ],
    sidebar,
    outline: [2, 3],
    docFooter: { prev: true, next: true },
    lastUpdatedText: '最后更新',
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    search: {
      provider: 'local',
      options: {
        locales: {
          'zh-CN': { placeholder: '搜索文档', noDataText: '无结果', headingDepth: 4 },
        },
      },
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Maicarons/mapcn-book' },
    ],
    footer: {
      message: '基于 mapcn 官方文档整理 · AI 辅助编撰',
      copyright: 'Copyright © 2026 Mapcn 从入门到进阶 编撰团队',
    },
  },
})
