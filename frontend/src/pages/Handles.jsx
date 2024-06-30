import Heading from "../ui/Heading.jsx";
import Form from "../ui/Form.jsx";
import Input from "../ui/Input.jsx";
import FileInput from "../ui/FileInput.jsx";
import FormElement from "../ui/FormElement.jsx";
import Button from "../ui/Button.jsx";
import { FaDatabase } from "react-icons/fa6";
import { useForm } from "react-hook-form";
import { useRef } from "react";

function Handles() {
  const ref = useRef(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const watchFileInput = watch("file");

  const onSubmit = (data) => console.log(data);

  return (
    <>
      <Heading as="h1">
        <FaDatabase />
        Edit Handles
      </Heading>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Heading as="h2">Choose one of the options</Heading>
        <FormElement label="File from Local Storage" type="file">
          <FileInput
            edited={watchFileInput && true}
            text={watchFileInput ? watchFileInput[0].name : "*.csv, *.xls, *.xlsx"}
            ref={ref}
            {...register("file")}
          />
        </FormElement>
        <FormElement label="Link to Google Sheets">
          <Input
            placeholder="https://docs.google.com/spreadsheets/..."
            {...register("link")}
          />
        </FormElement>
        <Button as="input" type="submit" value="Submit" />
      </Form>
    </>
  );
}

export default Handles;
