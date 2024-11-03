const PageLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="w-full md:max-w-[768px] lg:max-w-[1080px] pl-8 pt-12 m-auto">
      {children}
    </div>
  );
};

export default PageLayout;
