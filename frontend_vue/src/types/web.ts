// Achievement

export interface Achievement {
  id: number;
  name: string;
  description: string;
  category: string;
  key: string;
  image_url: string;
}

// Student

export interface Version {
  id: number;
  name: string;
}

export interface School {
  id: number;
  name: string;
  image_url: string;
}

export interface Student {
  id: number;
  name: string;
  rarity: number;
  is_limited: boolean;
  version: Version;
  school: School;
  portrait_url: string;
  artwork_url: string;
}

// Gacha

export interface Preset {
  id: number;
  name: string;
  pickup_rate: number;
  r3_rate: number;
  r2_rate: number;
  r1_rate: number;
}

export interface Banner {
  id: number;
  name: string;
  include_limited: boolean;
  preset: Preset;
  image_url: string;
}

export interface BannerDetail extends Banner {
  pickup_r3_students: Student[];
  nonpickup_r3_students: Student[];
  r2_students: Student[];
  r1_students: Student[];
}

export interface Result {
  student: Student;
  is_pickup: boolean;
  is_new: boolean;
}

export interface GachaPull {
  results: Result[];
  unlocked_achievements: Achievement[];
}

// Dashboard (Summary)

export interface FirstR3 {
  student: Student;
  first_obtain_on: Date | string; 
}

export interface Top3Student {
  student: Student;
  count: number;
  first_obtained: Date | string;
}

interface RarityCounter {
  r3_count: number
  r2_count: number
  r1_count: number
}

export interface Kpi extends RarityCounter {
  total_pulls: number
  total_pyroxene_spent: number
}

export interface BannerDistribution {
  data: Record<string, RarityCounter>;
}

interface SummaryEntry {
  obtained: number;
  total: number;
}

export interface SummaryCollectionResponse {
  data: Record<string, SummaryEntry>;
}

export interface MileStone {
  pull_number: number;
  student: Student;
}

interface LuckGaps {
  min: number;
  max: number;
  avg: number;
}

export interface LuckPerformance {
  banner_name: string;
  total_pulls: number;
  r3_count: number;
  user_rate: number;
  banner_rate: number;
  luck_variance: number;
  gaps: LuckGaps | null;
}

// Dashboard (History)

export interface Transaction {
  id: number;
  create_on: Date | string; 
  student: Student;
  banner: Banner;
}

export interface History {
  total_pages: number;
  current_page: number;
  items: Transaction[];
}