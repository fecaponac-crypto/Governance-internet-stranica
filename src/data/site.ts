// Site-wide configuration. Category ids must match data/sources.yaml.

export const SITE = {
  name: 'Data Governance Signal',
  shortName: 'DG Signal',
  tagline: 'What matters in data governance, and why.',
  description:
    'An independent, editor-reviewed briefing on data governance, privacy, AI governance and data regulation — with the context professionals need to act.',
  url: 'https://datagovernancesignal.com',
  email: 'editor@datagovernancesignal.com',
  // Buttondown newsletter (double opt-in, open/click tracking off).
  newsletterSubscribeUrl: 'https://buttondown.com/api/emails/embed-subscribe/datagovernancesignal',
  newsletterArchiveUrl: 'https://buttondown.com/datagovernancesignal',
  // While true: preview banner on every page, noindex, robots.txt disallows crawling.
  preview: true,
};

// Weekly editor's column; the newsletter goes out with it on Mondays.
export const COLUMN = {
  name: 'The Monday Signal',
  // Pen name of the editor (a practitioner who works in the field).
  author: 'The Steward',
  authorBio:
    'The Steward is the pen name of the editor of Data Governance Signal — a practitioner in master data management since 2011 and in data governance since 2019, with governance leadership and AI governance roles.',
};

// Where a development stands. Shown on every article that has one; explained on /methodology/.
export const STATUS_STAGES: Record<string, string> = {
  Proposal: 'Proposed law, rule or designation — not adopted; the text can change.',
  'In negotiation': 'Legislators or parties are negotiating; positions are not final.',
  Consultation: 'Open for comments; nothing has been decided yet.',
  Investigation: 'An authority has opened an inquiry or sent requests; no decision yet.',
  Adopted: 'Formally adopted, but obligations do not apply yet (or not all of them).',
  'In force': 'Obligations apply now.',
  Decision: 'A final decision by an authority (e.g. a fine or order); it may still be appealed in court.',
  'Court ruling': 'A judgment by a court; check whether it can be appealed.',
  'Non-binding opinion': 'An opinion that informs a decision but does not bind (e.g. an Advocate General opinion).',
  Published: 'Guidance, a standard, a report or research has been published.',
  Announced: 'Announced by the company or body, but not yet available or effective.',
  Preview: 'Available as a preview or beta; may change before general availability.',
  Available: 'Generally available.',
  Alleged: 'Claims made by a party (a complaint, lawsuit or advocacy) that no authority or court has ruled on.',
  Unconfirmed: 'Reported by the media but not confirmed by the parties or an official source.',
};
export const STATUS_IDS = Object.keys(STATUS_STAGES) as [string, ...string[]];

export const PREDICTION_STATUSES = ['open', 'correct', 'partly', 'wrong', 'void'] as const;

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
