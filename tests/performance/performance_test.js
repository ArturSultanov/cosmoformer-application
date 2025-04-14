import http from 'k6/http';
import { check, sleep } from 'k6';

let TARGET_URL = __ENV.TARGET_URL || '';
if (TARGET_URL.startsWith("http://")) {
  TARGET_URL = TARGET_URL.replace("http://", "https://");
}

const imagesList = JSON.parse(__ENV.IMAGES_JSON);

const fileDataMap = {};
for (let i = 0; i < imagesList.length; i++) {
  const fname = imagesList[i];
  fileDataMap[fname] = open(`../images/${fname}`, 'b');
}


export const options = {
  scenarios: {
    performace_test: {
      executor: 'ramping-vus',
      exec: 'performTest',
      startVUs: 0,
      stages: [
        { duration: '15s', target: 5 },
        { duration: '15s', target: 5 },
        { duration: '10s', target: 0 },
      ],
      gracefulStop: '5s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(90)<1000', 'p(95)<2000'],
  },
};

export function performTest() {
  makeRequest();
  sleep(1);
}

function makeRequest() {
  const randomIndex = Math.floor(Math.random() * imagesList.length);
  const filename = imagesList[randomIndex];
  const fileContent = fileDataMap[filename];
  const fileField = http.file(fileContent, filename, 'image/jpeg');

  const payload = { file: fileField };
  const res = http.post(TARGET_URL, payload);
  console.log(`Response for ${filename}: status ${res.status}, body: ${res.body}`);

  check(res, {
    'status was 200': (r) => r.status === 200,
    'response time < 2s': (r) => r.timings.duration < 2000,
  });
}