const express = require("express");
const { execSync } = require("child_process");
const os = require("os");
const fs = require("fs");

const app = express();
const port = 5000;

const formatUptime = () => {
  const uptimeSeconds = parseFloat(
    fs.readFileSync("/proc/uptime", "utf8").split(" ")[0]
  ); // Read uptime in seconds
  const uptimeMinutes = (uptimeSeconds / 60).toFixed(2); // Convert uptime to minutes and format it
  return `${uptimeMinutes} minutes`;
};

const systemInfo = () => {
  try {
    const ip = execSync("hostname -i").toString().trim();
    const runningProcesses = execSync("ps -e").toString().trim();
    const diskSpace = execSync("df -h /").toString().trim();
    const uptime = formatUptime();

    return {
      "IP Address": ip,
      "Running Processes": runningProcesses,
      "Disk Space": diskSpace,
      Uptime: uptime,
    };
  } catch (error) {
    return { error: `Failed to retrieve system information: ${error.message}` };
  }
};

app.get("/system_info", (req, res) => {
  res.json(systemInfo());
});

app.listen(port, () => {
  console.log(`Service2 listening at http://localhost:${port}`);
});
