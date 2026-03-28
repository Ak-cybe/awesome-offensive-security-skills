#!/usr/bin/env node
/**
 * generate-index.js — Auto-generates index.json from all SKILL.md files
 * Usage: node generate-index.js [--validate]
 */

const fs = require('fs');
const path = require('path');
const yaml = require('yaml'); // fallback to manual parse if not available

const SKILLS_DIR = path.join(__dirname, 'skills');
const OUTPUT = path.join(__dirname, 'index.json');

function parseYamlFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const lines = match[1].split(/\r?\n/);
  const result = {};
  let currentKey = null;
  let currentValue = '';
  
  for (const line of lines) {
    const keyMatch = line.match(/^(\w[\w_-]*)\s*:\s*(.*)/);
    if (keyMatch) {
      if (currentKey) {
        result[currentKey] = parseValue(currentValue.trim());
      }
      currentKey = keyMatch[1];
      currentValue = keyMatch[2];
    } else if (currentKey && (line.startsWith('  ') || line.startsWith('\t'))) {
      currentValue += '\n' + line;
    }
  }
  if (currentKey) {
    result[currentKey] = parseValue(currentValue.trim());
  }
  return result;
}

function parseValue(val) {
  if (!val) return '';
  // Array
  if (val.startsWith('[') && val.endsWith(']')) {
    return val.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
  }
  // Quoted string
  if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
    return val.slice(1, -1);
  }
  return val;
}

function scanSkills(dir, relative = '') {
  const skills = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const skillPath = path.join(dir, entry.name);
    const skillMd = path.join(skillPath, 'SKILL.md');
    
    if (fs.existsSync(skillMd)) {
      const content = fs.readFileSync(skillMd, 'utf-8');
      const meta = parseYamlFrontmatter(content);
      if (meta) {
        skills.push({
          name: meta.name || entry.name,
          description: typeof meta.description === 'string' ? meta.description : '',
          domain: meta.domain || 'cybersecurity',
          subdomain: meta.subdomain || '',
          category: meta.category || '',
          difficulty: meta.difficulty || '',
          tags: Array.isArray(meta.tags) ? meta.tags : [],
          tools: Array.isArray(meta.tools) ? meta.tools : [],
          version: meta.version || '1.0',
          author: meta.author || 'CyberSkills-Elite',
          license: meta.license || 'Apache-2.0',
          path: path.join('skills', relative, entry.name).replace(/\\/g, '/')
        });
      }
    } else {
      // Recurse into subcategory directories
      const subRelative = relative ? path.join(relative, entry.name) : entry.name;
      skills.push(...scanSkills(skillPath, subRelative));
    }
  }
  return skills;
}

function validate(skills) {
  let errors = 0;
  for (const skill of skills) {
    if (!skill.name) { console.error(`ERROR: Missing name in ${skill.path}`); errors++; }
    if (!skill.description || skill.description === '>' || skill.description.length < 20) {
      console.error(`ERROR: Bad description in ${skill.path}: "${skill.description}"`); errors++;
    }
    if (!skill.subdomain) { console.error(`WARN: Missing subdomain in ${skill.path}`); }
    if (!skill.tags || skill.tags.length === 0) { console.error(`WARN: No tags in ${skill.path}`); }
  }
  console.log(`\nValidation: ${skills.length} skills, ${errors} errors`);
  return errors === 0;
}

// Main
const skills = scanSkills(SKILLS_DIR);
const isValidate = process.argv.includes('--validate');

if (isValidate) {
  validate(skills);
  process.exit(0);
}

// Build stats
const subdomainStats = {};
const tagCounts = {};
const difficultyStats = {};

for (const s of skills) {
  if (s.subdomain) subdomainStats[s.subdomain] = (subdomainStats[s.subdomain] || 0) + 1;
  if (s.difficulty) difficultyStats[s.difficulty] = (difficultyStats[s.difficulty] || 0) + 1;
  for (const t of s.tags) tagCounts[t] = (tagCounts[t] || 0) + 1;
}

const topTags = Object.entries(tagCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 25)
  .map(([tag, count]) => ({ tag, count }));

const index = {
  version: '1.0.0',
  generated_at: new Date().toISOString(),
  repository: 'https://github.com/Ak-cybe/awesome-offensive-security-skills',
  total_skills: skills.length,
  total_subdomains: Object.keys(subdomainStats).length,
  subdomain_stats: subdomainStats,
  difficulty_stats: difficultyStats,
  top_tags: topTags,
  skills: skills.sort((a, b) => a.name.localeCompare(b.name))
};

fs.writeFileSync(OUTPUT, JSON.stringify(index, null, 2));
console.log(`Generated index.json with ${skills.length} skills`);
validate(skills);
