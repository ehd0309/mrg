import { Divider } from "@nextui-org/react";

const PageTitle = ({ title }: { title: string }) => {
  return (
    <>
      <h2 className="text-2xl font-semibold py-4">{title}</h2>
      <Divider className="mb-4" />
    </>
  );
};

export default PageTitle;
