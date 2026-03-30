#!/bin/bash

echo "🔄 Adding files..."
git add .

echo "📝 Committing..."
git commit -m "auto update $(date '+%Y-%m-%d %H:%M:%S')"

echo "🚀 Pushing to GitHub..."
git push

echo "✅ Done!"
