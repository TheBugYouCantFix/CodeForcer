import toast from "react-hot-toast";
import { useForm } from "react-hook-form";
import Form from "../../ui/Form";
import Heading from "../../ui/Heading";
import FileInput from "../../ui/FileInput";
import Button from "../../ui/Button";
import FormElement from "../../ui/FormElement";
import { uploadHandlesFile } from "../../api/handles";
import { useState } from "react";
import SpinnerMini from "../../ui/SpinnnerMini";
// import Input from "../../ui/Input";
// import styled from "styled-components";

// const Error = styled.span`
//   display: flex;
//   justify-content: center;
//   text-align: center;
//   font-size: 1.4rem;
//   color: var(--color-red-400);
// `;

export default function FormFileUpdate() {
  const {
    register,
    handleSubmit,
    watch,
    // setError,
    reset,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  const [isGetting, setIsGetting] = useState(false);
  function onSubmit({ file }) {
    // if (file.length === 0 && link.trim().length == 0) {
    //   setError("neitherItem", {
    //     type: "manual",
    //     message: "You must fill out either file or link field",
    //   });
    //   return;
    // }
    setIsGetting(true);
    uploadHandlesFile(file[0])
      .then((res) => {
        return res.json();
      })
      .then(({ updated, created }) => {
        const message =
          updated && created
            ? `updated: ${updated}, created: ${created}`
            : updated
              ? `updated: ${updated}`
              : created
                ? `created: ${created}`
                : "";
        toast.success(`Successfully ${message}`);
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
          text={watchFileInput?.length ? watchFileInput[0]?.name : "*.csv"}
          accept={".csv"}
          register={register("file", { required: "This field is required" })}
          disabled={isGetting}
        />
      </FormElement>
      {/*<FormElement label="Link to Google Sheets">
        <Input
          disabled={isGetting}
          placeholder="https://docs.google.com/spreadsheets/..."
          {...register("link")}
        />
      </FormElement>
      {errors.neitherItem && <Error>{errors?.neitherItem.message}</Error>}
      */}
      <Button disabled={isGetting} type="submit">
        {isGetting ? <SpinnerMini /> : "Submit"}
      </Button>
    </Form>
  );
}
