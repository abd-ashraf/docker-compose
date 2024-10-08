const express = require("express");
const { execSync } = require("child_process");
const os = require("os");

const app = express();
const port = 5000;

// Helper function to parse disk space using `df` and format it
const getFormattedDiskSpace = () => {
  const diskInfo = execSync("df -k /").toString().trim(); // Get raw disk usage in KB
  const lines = diskInfo.split("\n"); // Split output into lines
  const diskLine = lines[1]; // Get the line with disk information (usually the second line)

  // Split the line into fields and extract total, used, and available space (in KB)
  const fields = diskLine.split(/\s+/);
  const totalKB = parseInt(fields[1], 10);
  const usedKB = parseInt(fields[2], 10);
  const availableKB = parseInt(fields[3], 10);

  // Convert to GB and format
  const totalGB = (totalKB / 1024 ** 2).toFixed(2); // Convert KB to GB
  const usedGB = (usedKB / 1024 ** 2).toFixed(2);
  const availableGB = (availableKB / 1024 ** 2).toFixed(2);

  return `Total: ${totalGB}GB, Used: ${usedGB}GB, Free: ${availableGB}GB`;
};

const formatUptime = () => {
  const uptimeSeconds = os.uptime(); // Get the uptime in seconds
  const uptimeHours = (uptimeSeconds / 3600).toFixed(2); // Convert uptime to hours and format it
  return `${uptimeHours} hours`; // Return formatted uptime in hours
};

const systemInfo = () => {
  const networkInterfaces = os.networkInterfaces();
  const ip =
    Object.values(networkInterfaces)
      .flat()
      .find((iface) => !iface.internal && iface.family === "IPv4")?.address ||
    "N/A";

  const runningProcesses = execSync("ps -e").toString().trim();
  const diskSpace = getFormattedDiskSpace();
  const uptime = formatUptime()

  return {
    "IP Address": ip,
    "Running Processes": runningProcesses,
    "Disk Space": diskSpace,
    "Uptime (seconds)": uptime,
  };
};

app.get("/system_info", (req, res) => {
  res.json(systemInfo());
});

app.listen(port, () => {
  console.log(`Service2 listening at http://localhost:${port}`);
});
