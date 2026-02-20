export interface Achievement {
  id: number;
  name: string;
  description: string;
  category: string;
  key: string;
  image_url: string;
}

export interface Version {
  id: number;
  name: string;
}

export interface Preset {
  id: number;
  name: string;
  pickup_rate: number;
  r3_rate: number;
  r2_rate: number;
  r1_rate: number;
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

export interface FirstR3 {
  student: Student;
  first_obtain_on: Date | string; 
}

export interface Top3Student {
  student: Student;
  count: number;
  first_obtained: Date | string;
}

export interface Kpi {
  r3_count: number
  r2_count: number
  r1_count: number
  total_pulls: number
  total_pyroxene_spent: number
}

export interface GachaPull {
  results: Result[];
  unlocked_achievements: Achievement[];
}
