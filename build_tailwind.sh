#!/bin/bash

# Project Lima – Tailwind Build (No init)
# ✅ For Tailwind CLI v4.1.11+ on Amazon Linux 2023
# ✅ Golden Rule #6 Compliant

cd ~/project_lima

# Ensure required folders exist
mkdir -p static/src static/dist/css

# Recreate static/src/input.css (in case missing)
cat > static/src/input.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Recreate tailwind.config.js (manually)
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

# Build Tailwind output file
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
