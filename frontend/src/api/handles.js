export async function uploadHandlesFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  const url = `/api/students/file`;

  const response = await fetch(url, {
    method: "PATCH",
    body: formData,
  });

  console.log("File uploading response: ", response);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return response;
}

export async function uploadSingleHandle(info) {
  const url = `/api/students/${info.email}`;

  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(info),
  });
  console.log("Single handle uploading response: ", response);

  if (!response.ok) {
    if (response.status == 400) {
      const error = new Error("User with handle ");
      error.code = response.status;
      error.handle = info.handle;
      throw error;
    }
    throw new Error(response.statusText);
  }

  return response;
}
