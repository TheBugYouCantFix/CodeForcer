import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import Form from "../../ui/Form";
import Heading from "../../ui/Heading";
import FileInput from "../../ui/FileInput";
import Button from "../../ui/Button";
import FormElement from "../../ui/FormElement";
import { uploadHandlesFile, uploadFromSheet } from "../../api/handles";
import { useState } from "react";
import SpinnerMini from "../../ui/SpinnnerMini";

export default function FormFileUpdate() {
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  function handleGoogleClick() {
    setIsGetting(true);
    uploadFromSheet()
      .then(({ updated, created }) => {
        toast.success(
          updated && created
            ? `Updated: ${updated}\nCreated: ${created}`
            : updated
              ? `Updated: ${updated}`
              : created
                ? `Created: ${created}`
                : "Nothing new :)",
        );
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => setIsGetting(false));
  }

  const [isGetting, setIsGetting] = useState(false);
  function onSubmit({ file }) {
    setIsGetting(true);
    uploadHandlesFile(file[0])
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        toast.success(
          `Successfully updated ${data.length ? data.length + " items" : ""}`,
        );
        reset();
      })
      .catch((err) => {
        toast.error(err.message);
      })
      .finally(() => {
        setIsGetting(false);
      });
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Heading as="h2">Update with file</Heading>
      <FormElement
        label="File from Local Storage"
        type="file"
        error={errors?.file?.message}
      >
        <FileInput
          edited={watchFileInput && "true"}
          text={watchFileInput ? watchFileInput[0]?.name : "*.csv"}
          accept={".csv"}
          register={register("file")}
          disabled={isGetting}
        />
        <Button
          disabled={isGetting}
          type="submit"
          style={{ width: "100%", marginTop: "2.5rem" }}
        >
          {isGetting ? <SpinnerMini /> : "Submit"}
        </Button>
      </FormElement>
      <Heading as="h2">Update with connected Google Sheet</Heading>
      <Button onClick={handleGoogleClick} disabled={isGetting} type="button">
        {isGetting ? <SpinnerMini /> : "Update from Sheet"}
      </Button>
    </Form>
  );
}
