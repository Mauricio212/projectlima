#!/bin/bash

# Project Lima - Day 1, Hour 1-2: Tailwind CSS Setup for Amazon Linux 2023
# ✅ OS Certified: Amazon Linux 2023 (dnf-based)
# ✅ Golden Rule #6 Compliant

cd ~/project_lima

# Install Node.js & npm using Amazon Linux 2023 repo
sudo dnf install -y nodejs npm

# Initialize npm and install Tailwind CSS
npm init -y
npm install tailwindcss @tailwindcss/cli --save-dev

# Create Tailwind config
npx tailwindcss init

# Create folder structure
mkdir -p static/src static/dist/css templates

# Create Tailwind base input file
cat > static/src/input.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Configure tailwind.config.js
cat > tailwind.config.js << 'EOF'
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
