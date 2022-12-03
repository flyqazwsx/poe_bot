## bot使用main.py
    使用class
    @bot.even 要改成 @commands.Cog.listener()
## Discord 2.0
    async def setup(bot):            前面要加 async
        await bot.add_cog(poe(bot))  前面要加 await
    要加await
