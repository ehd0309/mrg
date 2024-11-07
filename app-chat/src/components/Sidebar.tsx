import { api } from "@/api";
import { Button, Divider } from "@nextui-org/react";
import Image from "next/image";
import Link from "next/link";

const Sidebar = async () => {
  const keys = await api.getRagList();
  return (
    <div
      className="!w-[300px] bg-default-800 text-white py-4 flex flex-col min-h-[calc(100vh)]"
      style={{ position: "sticky", left: 0, top: 0 }}
    >
      <Link
        href="/"
        className="px-10 pb-4 border-none text-default-400 hover:text-default-100 flex gap-1"
      >
        <Image
          width={14}
          height={14}
          alt="dashboard"
          src="/images/dashboard.svg"
          style={{ transform: "translateY(1px)" }}
        />
        Dashboard
      </Link>
      <Divider className="bg-primary-200" />
      <br />
      <div className="px-10 pb-4">
        <p className="text-xs font-semibold text-default-400 -ml-2">
          Document List <span className="text-[8px]">▼</span>
        </p>
        {keys?.map((key: string) => (
          <div key={key}>
            <Link
              href={"/chat/" + key}
              className="my-4 border-none text-white hover:text-default-400 flex"
            >
              ☉&nbsp;{key}
            </Link>
          </div>
        ))}
        <Divider className="bg-default-600 mt-8 mb-4" />
        <Button
          startContent={
            <Image
              src="/images/pdf.png"
              width={16}
              height={16}
              alt="pdf-image"
            />
          }
          fullWidth
          color="default"
          className="bg-black text-white"
          radius="none"
        >
          문서 등록
        </Button>
      </div>
    </div>
  );
};

export default Sidebar;
