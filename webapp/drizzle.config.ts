import { defineConfig } from 'drizzle-kit';

export default defineConfig({
	schema: './src/lib/server/schema.ts',
	dialect: 'sqlite',
	dbCredentials: { 
		url: '../data/posts.db'
	},
	verbose: true,
	strict: true
});
