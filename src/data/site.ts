// Site-wide configuration. Category ids must match data/sources.yaml.

export const SITE = {
  name: 'Data Governance Signal',
  shortName: 'DG Signal',
  tagline: 'What matters in data governance, and why.',
  description:
    'An independent, editor-reviewed briefing on data governance, privacy, AI governance and data regulation — with the context professionals need to act.',
  url: 'https://datagovernancesignal.com',
  email: 'editor@datagovernancesignal.com',
  // While true: preview banner on every page, noindex, robots.txt disallows crawling.
  preview: true,
};

export type Section = 'core' | 'broad';

export interface Category {
  id: string;
  label: string;
  short: string;
  section: Section;
  description: string;
}

export const CATEGORIES: Category[] = [
  {
    id: 'regulation',
    label: 'Regulation & Compliance',
    short: 'Regulation',
    section: 'core',
    description: 'EU AI Act, Data Act, GDPR reform, DORA, NIS2 and the rules shaping how organisations use data.',
  },
  {
    id: 'privacy',
    label: 'Privacy & Data Protection',
    short: 'Privacy',
    section: 'core',
    description: 'Enforcement, guidance and court decisions on personal data — and what they mean in practice.',
  },
  {
    id: 'ai-governance',
    label: 'AI Governance',
    short: 'AI Governance',
    section: 'core',
    description: 'Oversight of AI models and agents, responsible AI, standards such as ISO/IEC 42001.',
  },
  {
    id: 'strategy',
    label: 'Strategy & Operating Models',
    short: 'Strategy',
    section: 'core',
    description: 'Frameworks, organisation, roles, maturity and the business value of governed data.',
  },
  {
    id: 'data-quality',
    label: 'Data Quality',
    short: 'Data Quality',
    section: 'core',
    description: 'Measuring and improving data quality, observability, anonymisation and data fitness for use.',
  },
  {
    id: 'metadata',
    label: 'Metadata, Catalogs & Lineage',
    short: 'Metadata',
    section: 'core',
    description: 'Data catalogs, business glossaries, lineage, semantic layers and context for AI.',
  },
  {
    id: 'mdm',
    label: 'Master & Reference Data',
    short: 'Master Data',
    section: 'core',
    description: 'MDM, reference data, golden records and data products.',
  },
  {
    id: 'security',
    label: 'Security & Access',
    short: 'Security',
    section: 'core',
    description: 'Access governance, data classification, breaches and data security posture.',
  },
  {
    id: 'market',
    label: 'Vendors & Market',
    short: 'Market',
    section: 'core',
    description: 'Product launches, acquisitions, funding and analyst research across the governance market.',
  },
  {
    id: 'platforms',
    label: 'Data Platforms & Architecture',
    short: 'Platforms',
    section: 'broad',
    description: 'Lakehouse, data mesh, data fabric and the platforms governance runs on.',
  },
  {
    id: 'analytics',
    label: 'Analytics & BI',
    short: 'Analytics',
    section: 'broad',
    description: 'Analytics and BI developments with a governance angle.',
  },
  {
    id: 'ai-industry',
    label: 'AI Industry',
    short: 'AI Industry',
    section: 'broad',
    description: 'AI industry news that affects how data is governed.',
  },
];

export const CATEGORY_IDS = CATEGORIES.map((c) => c.id) as [string, ...string[]];

export const categoryById = (id: string): Category => {
  const c = CATEGORIES.find((c) => c.id === id);
  if (!c) throw new Error(`Unknown category: ${id}`);
  return c;
};

// Main navigation (the rest is reachable via /topics/).
export const NAV_CATEGORIES = ['regulation', 'privacy', 'ai-governance', 'strategy', 'metadata', 'data-quality', 'market'];

export const CONTENT_TYPES = [
  'Regulation',
  'Enforcement',
  'Supervision',
  'Guidance',
  'Standard',
  'Research',
  'Product launch',
  'Acquisition',
  'Funding',
  'Case study',
  'Announcement',
  'Event',
] as const;

export const IMPORTANCE_LABELS: Record<number, string> = {
  1: 'Background',
  2: 'Worth knowing',
  3: 'Notable',
  4: 'Important',
  5: 'Critical',
};
